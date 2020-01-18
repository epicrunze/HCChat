import webhook
WEBHOOK_URL="https://praxis-atrium-265504.appspot.com/test-post"
AUTH="cd5a0a3d9909103835b100851a2b6fe528b8114b"
print(webhook.addWebhook(WEBHOOK_URL,AUTH))
#print(webhook.removeWebhook(AUTH))
