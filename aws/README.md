Logging In and Testing

In AWS set up an API Gateway with a Cognito Authorizer
https://www.youtube.com/watch?v=Qvx3HRBFIGs

oidcdebugger.com
Authorize URI: https://yatesee.auth.us-west-2.amazoncognito.com/oauth2/authorize
Redirect URI: https://oidcdebugger.com/debug Client ID: 538krug2293i7vqj9adiaa9dkv
Scope: openid
Response type: code

This should give an Auth code Plug this into the token call in Postman for code to get tokens
POST https://dev-30912539.okta.com/oauth2/v1/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code=5aa6686b-4f67-4a83-9f87-3f6b92736131&
client_id=538krug2293i7vqj9adiaa9dkv&
client_secret={clientSecret}&
redirect_uri=https%3A%2F%2Foidcdebugger.com%2Fdebug

Copy the id_token to the Bearer token in the New Game call.


Design Notes:
Lambda vs Lambda Proxy
https://medium.com/@lakshmanLD/lambda-proxy-vs-lambda-integration-in-aws-api-gateway-3a9397af0e6d
Used Lambda Proxy

