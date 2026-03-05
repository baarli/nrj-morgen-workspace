// Supabase Edge Function: voice-chat v2.0
// Med ElevenLabs TTS integrasjon

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

// ElevenLabs config
const ELEVENLABS_API_KEY = Deno.env.get('ELEVENLABS_API_KEY')
const VEV_VOICE_ID = Deno.env.get('VEV_VOICE_ID') || 'JBFqnCBsd6RMkjVDRZzb'
const VEV_VOICE_MODEL = Deno.env.get('VEV_VOICE_MODEL') || 'eleven_flash_v2_5'

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { text, user_id, session_id } = await req.json()
    
    console.log('🎤 Voice chat request:', { text, user_id, session_id })
    
    if (!text || !user_id) {
      return new Response(
        JSON.stringify({ error: 'Missing required fields' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    // Lagre brukerens melding
    await supabaseClient
      .from('voice_chat_messages')
      .insert({
        user_id,
        session_id,
        text,
        sender: 'user',
        created_at: new Date().toISOString()
      })

    // Send til Vev og få svar
    const vevResponse = await sendToVev(text)
    
    // Generer TTS for Vevs svar
    const audioUrl = await generateTTS(vevResponse.text)
    
    // Lagre Vevs svar med audio URL
    await supabaseClient
      .from('voice_chat_messages')
      .insert({
        user_id,
        session_id,
        text: vevResponse.text,
        sender: 'vev',
        audio_url: audioUrl,
        created_at: new Date().toISOString()
      })

    return new Response(
      JSON.stringify({
        success: true,
        text: vevResponse.text,
        audio_url: audioUrl
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )

  } catch (error) {
    console.error('Error:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})

async function sendToVev(text) {
  // Forenklet versjon - i produksjon ville dette kalle OpenClaw
  // For nå, genererer vi et naturlig svar
  
  const responses = [
    "Det er interessant! Fortell meg mer.",
    "Jeg forstår. Hva tenker du om det?",
    "Det gir mening. Har du vurdert alternativene?",
    "Jeg hører deg. La meg tenke på det...",
    "Bra poeng! Jeg er enig.",
  ]
  
  // Velg respons basert på tekst (hash)
  const hash = text.split('').reduce((a, b) => a + b.charCodeAt(0), 0)
  const response = responses[hash % responses.length]
  
  return { text: response }
}

async function generateTTS(text) {
  if (!ELEVENLABS_API_KEY) {
    console.log('⚠️ No ElevenLabs API key, skipping TTS')
    return null
  }
  
  try {
    const url = `https://api.elevenlabs.io/v1/text-to-speech/${VEV_VOICE_ID}`
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'audio/mpeg',
        'Content-Type': 'application/json',
        'xi-api-key': ELEVENLABS_API_KEY
      },
      body: JSON.stringify({
        text: text,
        model_id: VEV_VOICE_MODEL,
        voice_settings: {
          stability: 0.5,
          similarity_boost: 0.75
        }
      })
    })
    
    if (!response.ok) {
      console.error('ElevenLabs error:', response.status)
      return null
    }
    
    // Lagre audio til Supabase Storage
    const audioBlob = await response.blob()
    const fileName = `vev_${Date.now()}.mp3`
    
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )
    
    const { data, error } = await supabaseClient
      .storage
      .from('voice-chat-audio')
      .upload(fileName, audioBlob, {
        contentType: 'audio/mpeg'
      })
    
    if (error) {
      console.error('Storage error:', error)
      return null
    }
    
    // Få public URL
    const { data: urlData } = supabaseClient
      .storage
      .from('voice-chat-audio')
      .getPublicUrl(fileName)
    
    return urlData.publicUrl
    
  } catch (error) {
    console.error('TTS error:', error)
    return null
  }
}
