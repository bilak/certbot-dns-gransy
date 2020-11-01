# Gransi (Subreg) Authenticator certbot plugin

## Install

`pip install certbot-dns-gransy`

## Run

```
certbot certonly \
      -a dns-gransy \
      --dns-gransy-credentials gransy.ini \
      --dns-gransy-propagation-seconds 900 \
      --no-self-upgrade \
      --keep-until-expiring --non-interactive --expand \
      --server https://acme-v02.api.letsencrypt.org/directory \
      --email=your@email.com \
      --agree-tos \
      -d "domain.tld"
```
