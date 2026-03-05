import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

/**
 * Telegram Webhook Handler for BaarliClaw
 * 
 * Denne funksjonen mottar meldinger fra Telegram og sender dem
 * videre til OpenClaw slik at BaarliClaw kan svare personlig.
 */

interface TelegramMessage {
  message_id: number;
  from?: {
    id: number;
    first_name: string;
    username?: string;
  };
  chat: {
    id: number;
    type: string;
    title?: string;
  };
  date: number;
  text?: string;
}

interface TelegramUpdate {
  update_id: number;
  message?: TelegramMessage;
  callback_query?: {
    id: string;
    from: {
      id: number;
      first_name: string;
    };
    data?: string;
  };
}

// Konfigurasjon
const OPENCLAW_WEBHOOK_URL = "https://kvniauxokdtmpvjtfnej.supabase.co/functions/v1/openclaw-bridge";

serve(async (req: Request) => {
  // CORS headers
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
    "Content-Type": "application/json",
  };

  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers });
  }

  if (req.method !== "POST") {
    return new Response(
      JSON.stringify({ error: "Method not allowed" }),
      { headers, status: 405 }
    );
  }

  try {
    // Parse incoming webhook data fra Telegram
    let update: TelegramUpdate;
    try {
      update = await req.json();
    } catch (e) {
      console.error("Failed to parse JSON:", e);
      return new Response(
        JSON.stringify({ ok: false, error: "Invalid JSON" }),
        { headers, status: 200 }
      );
    }
    
    console.log("📨 Received from Telegram:", JSON.stringify(update, null, 2));

    // Handle messages
    if (update.message) {
      const { message } = update;
      const chatId = message.chat.id;
      const text = message.text || "";
      const username = message.from?.username || message.from?.first_name || "Ukjent";
      const userId = message.from?.id;

      console.log(`💬 Message from ${username} (ID: ${userId}): ${text}`);

      // Send meldingen videre til OpenClaw bridge
      try {
        const bridgeResponse = await fetch(OPENCLAW_WEBHOOK_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            source: "telegram",
            chat_id: chatId,
            user_id: userId,
            username: username,
            message: text,
            timestamp: new Date().toISOString(),
          }),
        });

        if (!bridgeResponse.ok) {
          console.error("Bridge error:", await bridgeResponse.text());
          // Fortsett uansett - vi vil ikke miste meldingen
        }
      } catch (bridgeError) {
        console.error("Failed to forward to bridge:", bridgeError);
      }

      // Send en "typing" eller bekreftelse tilbake til bruker
      // (BaarliClaw vil svare via bridge når han er klar)
      await sendMessage(chatId, "⏳ Melding mottatt! BaarliClaw svarer straks...");
    }

    // Return success to Telegram
    return new Response(
      JSON.stringify({ ok: true }),
      { headers, status: 200 }
    );

  } catch (error) {
    console.error("❌ Error processing webhook:", error);
    
    return new Response(
      JSON.stringify({ ok: false, error: error.message }),
      { headers, status: 200 }
    );
  }
});

/**
 * Send a message back to Telegram
 */
async function sendMessage(chatId: number, text: string): Promise<void> {
  const botToken = Deno.env.get("TELEGRAM_BOT_TOKEN");
  
  if (!botToken) {
    console.error("TELEGRAM_BOT_TOKEN not set");
    return;
  }

  const url = `https://api.telegram.org/bot${botToken}/sendMessage`;
  
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: chatId,
        text: text,
        parse_mode: "HTML",
      }),
    });

    if (!response.ok) {
      console.error("Failed to send message:", await response.text());
    }
  } catch (error) {
    console.error("Error sending message:", error);
  }
}
