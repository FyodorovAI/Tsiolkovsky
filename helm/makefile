
deploy-helm:
	. ./../src/.env && \
	helm upgrade --install tsiolkovsky ./../../helm/fyodorov-service-base \
	-f ./values.yaml \
	--namespace fyodorov --create-namespace \
	--force \
	--set env.SUPABASE_PROJECT_URL=$${SUPABASE_PROJECT_URL} \
	--set env.SUPABASE_API_KEY=$${SUPABASE_API_KEY} \
	--set env.JWT_SECRET=$${JWT_SECRET}

uninstall-helm:
	helm uninstall tsiolkovsky
