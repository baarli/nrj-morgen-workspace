# Deploy Mission Control til nrjmorgen.com/kloakontroll

## Forutsetninger
- Du har tilgang til nrjmorgen.com webserver
- Du har FTP/SSH tilgang eller kontrollpanel (cPanel/Plesk)
- Du kan opprette undermappe /kloakontroll

## Metode 1: FTP/SSH Upload (Enklest)

### Steg 1: Koble til server
```bash
# Via SSH
ssh brukernavn@nrjmorgen.com

# Eller via FTP med FileZilla
Server: nrjmorgen.com
Brukernavn: (ditt brukernavn)
Passord: (ditt passord)
```

### Steg 2: Opprett mappe
```bash
# På serveren
mkdir -p /var/www/nrjmorgen.com/public_html/kloakontroll
# eller
cd public_html
mkdir kloakontroll
```

### Steg 3: Last opp filer
```bash
# Via SCP
scp -r /root/.openclaw/workspace/mission-control/build/* \
  brukernavn@nrjmorgen.com:/var/www/nrjmorgen.com/public_html/kloakontroll/

# Eller via FTP: Last opp index.html til /kloakontroll/
```

### Steg 4: Sett rettigheter
```bash
chmod 755 /var/www/nrjmorgen.com/public_html/kloakontroll
chmod 644 /var/www/nrjmorgen.com/public_html/kloakontroll/index.html
```

### Steg 5: Test
Åpne: https://nrjmorgen.com/kloakontroll

---

## Metode 2: cPanel (Hvis du bruker cPanel)

### Steg 1: Logg inn i cPanel
Gå til: nrjmorgen.com/cpanel

### Steg 2: Åpne File Manager
Klikk på "File Manager" ikonet

### Steg 3: Naviger til public_html
Dobbeltklikk på public_html mappen

### Steg 4: Opprett ny mappe
- Klikk "+ Folder" øverst
- Navn: kloakontroll
- Klikk "Create New Folder"

### Steg 5: Last opp fil
- Gå inn i kloakontroll mappen
- Klikk "Upload" øverst
- Velg index.html fra mission-control/build/
- Vent på at opplasting fullføres

### Steg 6: Test
Åpne: https://nrjmorgen.com/kloakontroll

---

## Metode 3: GitHub + Webhook (Avansert)

### Steg 1: Push til GitHub
```bash
cd /root/.openclaw/workspace/mission-control/build
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/dittbrukernavn/kloakontroll.git
git push -u origin main
```

### Steg 2: Sett opp webhook på server
Lag deploy script på serveren:
```bash
#!/bin/bash
cd /var/www/nrjmorgen.com/public_html/kloakontroll
git pull origin main
echo "Deployed at $(date)" >> deploy.log
```

### Steg 3: Konfigurer GitHub webhook
- Gå til GitHub repo → Settings → Webhooks
- Add webhook
- Payload URL: https://nrjmorgen.com/kloakontroll/deploy.php
- Content type: application/json
- Secret: (valgfritt)

---

## Passordbeskyttelse (htaccess)

Opprett .htaccess i kloakontroll mappen:
```apache
AuthType Basic
AuthName "Mission Control - Authorized Access Only"
AuthUserFile /var/www/nrjmorgen.com/.htpasswd
Require valid-user
```

Opprett .htpasswd:
```bash
htpasswd -cb /var/www/nrjmorgen.com/.htpasswd admin kloakontroll2026
```

---

## SSL/HTTPS (Hvis ikke allerede aktivert)

### Med Let's Encrypt:
```bash
certbot --nginx -d nrjmorgen.com
# eller
certbot --apache -d nrjmorgen.com
```

### Med cPanel:
- Gå til "SSL/TLS" i cPanel
- Klikk "Manage SSL Sites"
- Installer gratis Let's Encrypt sertifikat

---

## Feilsøking

### 404 Feil
- Sjekk at filen er i riktig mappe
- Sjekk at URL er korrekt: nrjmorgen.com/kloakontroll
- Sjekk at .htaccess ikke blokkerer

### 403 Feil
- Sjekk filrettigheter (skal være 644 for filer, 755 for mapper)
- Sjekk at index.html eksisterer

### Passord fungerer ikke
- Sjekk at .htpasswd path er korrekt i .htaccess
- Sjekk at .htpasswd filen eksisterer
- Regenerer passord: htpasswd -cb .htpasswd admin kloakontroll2026

---

## Support

Hvis du trenger hjelp med deploy, gi meg:
1. Hvilken hosting du bruker
2. Om du har SSH/FTP/cPanel tilgang
3. Eventuelle feilmeldinger

Så kan jeg guide deg mer spesifikt!
