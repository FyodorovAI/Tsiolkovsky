
deploy-helm:
	. ./../src/.env && \
	helm upgrade --install tsiolkovsky . --namespace fyodorov --create-namespace --dry-run \
	--set env.SUPABASE_PROJECT_URL=$${SUPABASE_PROJECT_URL} \
	--set env.SUPABASE_API_KEY=$${SUPABASE_API_KEY} \
	--set env.JWT_SECRET=$${JWT_SECRET}

uninstall-helm:
	helm uninstall tsiolkovsky