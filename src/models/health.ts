import { PostgrestError, SupabaseClient } from '@supabase/supabase-js';
import { isValidUrl } from './utils';

type UpdateType = {
    health_status: string;
    api_url?: string;
}

type HealthUpdateType = {
    tool_id: string;
    api_url?: string;
    health_status: string;
}

export class HealthUpdate {
    healthUpdate: HealthUpdateType

    constructor(update: HealthUpdateType) {
        HealthUpdate.validate(update);
        this.healthUpdate = update;
    }

    static validate(update: HealthUpdateType): void {
        if (!update.tool_id) {
            throw new Error('Tool ID is required');
        }
        if (!update.health_status) {
            throw new Error('Health status is required');
        }
        if (update.api_url) {
            if (!isValidUrl(update.api_url)) {
              throw new Error('New API URL is not valid');
            }
        }
    }

    toJSON() {
        return {
            tool_id: this.healthUpdate.tool_id,
            health_status: this.healthUpdate.health_status,
            extra: {
                api_url: this.healthUpdate.api_url
            }
        }
    }

    async updateToolInDB(supabase: SupabaseClient): Promise<PostgrestError | HealthUpdate> {
        let update: UpdateType = { health_status: this.healthUpdate.health_status };
        if (this.healthUpdate.api_url) {
            update.api_url = this.healthUpdate.api_url
        }
        const { data, error } = await supabase.from('tools')
                                    .update(update)
                                    .eq('id', this.healthUpdate.tool_id).select();
        if (error) {
            console.error(
              `Error updating tool with id ${this.healthUpdate.tool_id}` +
              ` and health status ${this.healthUpdate.health_status}` +
              ` with API URL ${this.healthUpdate.api_url}: ${error}`
            );
            return error;
        }
        else {
            const update = data[0];
            console.log('Updated tool with new API URL', update);
            return update;
        }
    }

    async saveHealthCheckInDB(supabase: SupabaseClient): Promise<PostgrestError | HealthUpdate> {
        const { data, error } = await supabase.from('tools_health_checks').insert(this.toJSON()).select();
        if (error) {
            console.error('Error saving health update', error);
            return error;
        }
        else {
            const update = data[0];
            console.log('Saved health update', update);
            return update;
        }
    }

    async saveHealthCheck(supabase: SupabaseClient): Promise<PostgrestError | HealthUpdate> {
        let promises = []
        if (this.healthUpdate.api_url) {
            promises.push(this.updateToolInDB(supabase));
        }
        promises.push(this.saveHealthCheckInDB(supabase));
        return Promise.all(promises)
            .then((results) => {
                return results[1] || results[0] as HealthUpdate;
            })
    }

    static async getHealthChecks(supabase: SupabaseClient, tool_id: string): Promise<PostgrestError | HealthUpdate[]> {
        const { data, error } = await supabase.from('tools_health_checks')
                                    .select('*').eq('tool_id', tool_id)
                                    .order('created_at', { ascending: false });
    if (error) {
        console.error('Error fetching health checks for tool', tool_id, error);
        return error
    } else {
        console.log('Fetched health checks for tool', tool_id, data);
        return data
    }
    }
}

