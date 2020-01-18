import webhook
REQUEST_BIN="https://praxis-atrium-265504.appspot.com/test-post"
WEBHOOK_URL="https://enjjibedx31jf.x.pipedream.net"
AUTH="cd5a0a3d9909103835b100851a2b6fe528b8114b"
print(webhook.addWebhook(WEBHOOK_URL,AUTH))
#print(webhook.removeWebhook(AUTH))
