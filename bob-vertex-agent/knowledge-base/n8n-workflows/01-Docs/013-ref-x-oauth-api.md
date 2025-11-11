# X (Twitter) OAuth API Reference

Complete OAuth API reference documentation saved for Claude AutoBlog SlashCommands project.

**Source:** https://developer.twitter.com/en/docs/authentication/api-reference
**Saved:** 2025-09-27
**Purpose:** Reference for implementing OAuth 1.0a and OAuth 2.0 authentication

---

## OAuth API Reference Index

### OAuth 1.0a
| Purpose | Method |
|---------|--------|
| Step 1 of the 3-legged OAuth flow and Sign in with X - Allows a Consumer application to obtain an OAuth Request Token to request user authorization. | `POST oauth/request_token` |
| Step 2 of the 3-legged OAuth flow and Sign in with X - Allows a Consumer application to use an OAuth Request Token to request user authorization. | `GET oauth/authenticate` |
| Step 2 of the 3-legged OAuth flow and Sign in with X - Allows a Consumer application to use an OAuth Request Token to request user authorization. | `GET oauth/authorize` |
| Step 3 of the 3-legged OAuth flow and Sign in with X - Allows a Consumer application to exchange the OAuth Request Token for an OAuth Access Token. | `POST oauth/access_token` |
| Allows a registered application to revoke an issued OAuth Access Token. | `POST oauth/invalidate_token` |

### OAuth 2.0 Bearer Token
| Purpose | Method |
|---------|--------|
| Allows a registered App to generate an OAuth 2 app-only Bearer Token, which can be used to make API requests on an App's behalf, without user context. | `POST oauth2/token` |
| Allows a registered App to revoke an issued OAuth 2 app-only Bearer Token. | `POST oauth2/invalidate_token` |

---

## POST oauth/request_token

Allows a Consumer application to obtain an OAuth Request Token to request user authorization. This method fulfills Section 6.1 of the OAuth 1.0 authentication flow.

**Important:** We require you use HTTPS for all OAuth authorization steps.
**Usage Note:** Only ASCII values are accepted for the oauth_nonce

**Resource URL:** `https://api.x.com/oauth/request_token`

**Resource Information:**
- Response formats: JSON
- Requires authentication?: No
- Rate limited?: Yes

**Parameters:**
- `oauth_callback` (required): For OAuth 1.0a compliance this parameter is required. The value you specify here will be used as the URL a user is redirected to should they approve your application's access to their account. Set this to `oob` for out-of-band pin mode. This is also how you specify custom callbacks for use in desktop/mobile applications. Always send an oauth_callback on this step, regardless of a pre-registered callback.
  - Examples: `http://themattharris.local/auth.php`, `twitterclient://callback`
- `x_auth_access_type` (optional): Overrides the access level an application requests to a users account. Supported values are `read` or `write`. This parameter is intended to allow a developer to register a read/write application but also request read only access when appropriate.

**Example request:**
```
Request URL: POST https://api.x.com/oauth/request_token
Request POST Body: N/A
Authorization Header: OAuth oauth_nonce="K7ny27JTpKVsTgdyLdDfmQQWVLERj2zAK5BslRsqyw", oauth_callback="http%3A%2F%2Fmyapp.com%3A3005%2Ftwitter%2Fprocess_callback", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1300228849", oauth_consumer_key="OqEqJeafRSF11jBMStrZz", oauth_signature="Pc%2BMLdv028fxCErFyi8KXFM%2BddU%3D", oauth_version="1.0"

Response: oauth_token=Z6eEdO8MOmk394WozF5oKyuAv855l4Mlqo7hhlSLik&oauth_token_secret=Kd75W4OQfb2oJTV0vzGzeXftVAwgMnEK9MumzYcM&oauth_callback_confirmed=true
```

---

## GET oauth/authorize

Allows a Consumer application to use an OAuth Request Token to request user authorization. This method fulfills Section 6.2 of the OAuth 1.0 authentication flow. Desktop applications must use this method (and cannot use GET oauth/authenticate).

**Usage Note:** An oauth_callback is never sent to this method, provide it to POST oauth/request_token instead.

**Resource URL:** `https://api.x.com/oauth/authorize`

**Resource Information:**
- Response formats: JSON
- Requires authentication?: Yes
- Rate limited?: Yes

**Parameters:**
- `force_login` (optional): Forces the user to enter their credentials to ensure the correct users account is authorized.
- `screen_name` (optional): Prefills the username input box of the OAuth login screen with the given value.

**Example request:**
```
Send the user to the oauth/authorize step in a web browser, including an oauth_token parameter:
https://api.x.com/oauth/authorize?oauth_token=Z6eEdO8MOmk394WozF5oKyuAv855l4Mlqo7hhlSLik
```

---

## GET oauth/authenticate

Allows a Consumer application to use an OAuth request_token to request user authorization.

This method is a replacement of Section 6.2 of the OAuth 1.0 authentication flow for applications using the callback authentication flow. The method will use the currently logged in user as the account for access authorization unless the force_login parameter is set to true.

This method differs from GET oauth/authorize in that if the user has already granted the application permission, the redirect will occur without the user having to re-approve the application. To realize this behavior, you must enable the Use Sign in with X setting on your application record.

**Resource URL:** `https://api.x.com/oauth/authenticate`

**Resource Information:**
- Response formats: JSON
- Requires authentication?: Yes
- Rate limited?: Yes

**Parameters:**
- `force_login` (optional): Forces the user to enter their credentials to ensure the correct users account is authorized.
  - Example: `true`
- `screen_name` (optional): Prefills the username input box of the OAuth login screen with the given value.

**Example request:**
```
Send the user to the oauth/authenticate step in a web browser, including an oauth_token parameter:
https://api.x.com/oauth/authenticate?oauth_token=Z6eEdO8MOmk394WozF5oKyuAv855l4Mlqo7hhlSLik
```

---

## POST oauth/access_token

Allows a Consumer application to exchange the OAuth Request Token for an OAuth Access Token. This method fulfills Section 6.3 of the OAuth 1.0 authentication flow.

**Resource URL:** `https://api.x.com/oauth/access_token`

**Resource Information:**
- Response formats: JSON
- Requires authentication?: Yes
- Rate limited?: Yes

**Parameters:**
- `oauth_token` (required): The oauth_token here must be the same as the oauth_token returned in the request_token step.
- `oauth_verifier` (required): If using the OAuth web-flow, set this parameter to the value of the oauth_verifier returned in the callback URL. If you are using out-of-band OAuth, set this value to the pin-code. For OAuth 1.0a compliance this parameter is required. OAuth 1.0a is strictly enforced and applications not using the oauth_verifier will fail to complete the OAuth flow.

**Example request:**
```
POST https://api.x.com/oauth/access_token?oauth_token=qLBVyoAAAAAAx72QAAATZxQWU6P&oauth_verifier=ghLM8lYmAxDbaqL912RZSRjCCEXKDIzx

From PIN-based:
POST https://api.x.com/oauth/access_token?oauth_token=9Npq8AAAAAAAx72QBRABZ4DAfY9&oauth_verifier=4868795
```

**Example response:**
```
oauth_token=6253282-eWudHldSbIaelX7swmsiHImEL4KinwaGloHANdrY&oauth_token_secret=2EEfA6BG5ly3sR3XjE0IBSnlQu4ZrUzPiYTmrkVU&user_id=6253282&screen_name=xapi
```

---

## POST oauth/invalidate_token

Allows a registered application to revoke an issued OAuth access_token by presenting its client credentials. Once an access_token has been invalidated, new creation attempts will yield a different Access Token and usage of the invalidated token will no longer be allowed.

**Resource URL:** `https://api.x.com/1.1/oauth/invalidate_token`

**Resource Information:**
- Response formats: JSON
- Requires authentication?: Yes - User context with the access tokens that you would like to invalidate
- Rate limited?: Yes

**Example request:**
```bash
curl --request POST \
  --url 'https://api.x.com/1.1/oauth/invalidate_token.json' \
  --header 'authorization: OAuth oauth_consumer_key="CLIENT_KEY",
     oauth_nonce="AUTO_GENERATED_NONCE", oauth_signature="AUTO_GENERATED_SIGNATURE",
     oauth_signature_method="HMAC-SHA1", oauth_timestamp="AUTO_GENERATED_TIMESTAMP",
     oauth_token="ACCESS_TOKEN", oauth_version="1.0"'
```

**Example response:**
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 127

{"access_token":"ACCESS_TOKEN"}
```

**Example error response after token has been invalidated:**
```
HTTP/1.1 401 Authorization Required

{"errors": [{
  "code": 89,
  "message": "Invalid or expired token."}
]}
```

---

## POST oauth2/token

Allows a registered application to obtain an OAuth 2 Bearer Token, which can be used to make API requests on an application's own behalf, without a user context. This is called Application-only authentication.

A Bearer Token may be invalidated using oauth2/invalidate_token. Once a Bearer Token has been invalidated, new creation attempts will yield a different Bearer Token and usage of the previous token will no longer be allowed.

Only one bearer token may exist outstanding for an application, and repeated requests to this method will yield the same already-existent token until it has been invalidated.

Successful responses include a JSON-structure describing the awarded Bearer Token.

Tokens received by this method should be cached. If attempted too frequently, requests will be rejected with a HTTP 403 with code 99.

**Resource URL:** `https://api.x.com/oauth2/token`

**Resource Information:**
- Response formats: JSON
- Requires authentication?: Yes - Basic auth with your API key as your username and API key secret as your password
- Rate limited?: Yes

**Parameters:**
- `grant_type` (required): Specifies the type of grant being requested by the application. At this time, only `client_credentials` is allowed. See Application-Only Authentication for more information.
  - Example: `client_credentials`

**Example request:**
```
POST /oauth2/token HTTP/1.1
Host: api.x.com
User-Agent: My X App v1.0.23
Authorization: Basic eHZ6MWV2R ... o4OERSZHlPZw==
Content-Type: application/x-www-form-urlencoded;charset=UTF-8
Content-Length: 29
Accept-Encoding: gzip

grant_type=client_credentials
```

**Example response:**
```
HTTP/1.1 200 OK
Status: 200 OK
Content-Type: application/json; charset=utf-8
Content-Encoding: gzip
Content-Length: 140

{"token_type":"bearer","access_token":"AAAA%2FAAA%3DAAAAAAAA"}
```

---

## POST oauth2/invalidate_token

Allows a registered application to revoke an issued oAuth 2.0 Bearer Token by presenting its client credentials. Once a Bearer Token has been invalidated, new creation attempts will yield a different Bearer Token and usage of the invalidated token will no longer be allowed.

Successful responses include a JSON-structure describing the revoked Bearer Token.

**Resource URL:** `https://api.x.com/oauth2/invalidate_token`

**Resource Information:**
- Response formats: JSON
- Requires authentication?: Yes - oAuth 1.0a with the application's consumer API keys and the application owner's access token & access token secret
- Rate limited?: Yes

**Parameters:**
- `access_token` (required): The value of the bearer token that you would like to invalidate

**Example request:**
```bash
curl --request POST \
  --url 'https://api.x.com/oauth2/invalidate_token?access_token=AAAA%2FAAA%3DAAAAAAAA' \
  --header 'authorization: OAuth oauth_consumer_key="CLIENT_KEY",
     oauth_nonce="AUTO_GENERATED_NONCE", oauth_signature="AUTO_GENERATED_SIGNATURE",
     oauth_signature_method="HMAC-SHA1", oauth_timestamp="AUTO_GENERATED_TIMESTAMP",
     oauth_token="ACCESS_TOKEN", oauth_version="1.0"'
```

**Example response:**
```
Status: 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 135

{
  "access_token": "AAAA%2FAAA%3DAAAAAAAA"
}
```

---

## Notes for Implementation

### Current Implementation Status
- ✅ **OAuth 2.0 Bearer Token** - Working for read operations
- ✅ **OAuth 1.0a posting** - Implementation complete in `scripts/post_x_thread.py`
- ❌ **3-legged OAuth flow** - Not needed for current use case (we have user tokens)

### Why We Use Direct OAuth 1.0a (Not 3-legged)
Our implementation uses OAuth 1.0a with pre-existing access tokens because:
1. User has already completed authorization in Twitter Developer Portal
2. We have all 5 required credentials (API key, secret, access token, access secret, bearer token)
3. No need for additional user authorization flow
4. Simpler implementation for automation scripts

### Authentication Summary
- **Read operations**: OAuth 2.0 Bearer Token (`X_BEARER_TOKEN`)
- **Write operations**: OAuth 1.0a with access tokens (`X_ACCESS_TOKEN`, `X_ACCESS_SECRET`)
- **Both require**: Consumer credentials (`X_API_KEY`, `X_API_SECRET`)

### Rate Limits
- **Essential access**: 75 requests per 15 minutes
- **Elevated access**: 100 requests per 15 minutes
- **Monthly limits**: 1,500 tweets per month (free tier)
- **Daily limits**: 50 tweets per day (free tier)

---

**Last Updated:** 2025-09-27
**Implementation:** Claude AutoBlog SlashCommands OAuth 1.0a posting
**Status:** Production ready (requires Elevated access for posting)