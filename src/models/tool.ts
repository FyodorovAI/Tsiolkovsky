import { PostgrestError, SupabaseClient } from '@supabase/supabase-js';

export type ToolType = {
    id?: string;
    name_for_human: string;
    name_for_ai: string;
    description_for_human: string;
    description_for_ai: string;
    api_type: string;
    api_url: string;
    logo_url: string;
    contact_email: string;
    legal_info_url: string;
}
export class Tool {
    tool: ToolType;

    constructor(tool: ToolType) {
        Tool.validate(tool);
        this.tool = tool;
    }
        
    update(tool: ToolType): void {
        const newTool = {...this.toJSON(), ...tool};
        Tool.validate(newTool);
        this.tool = newTool;
    }

    static validate(tool: ToolType): void {
        this.validateNameForHuman(tool);
        this.validateNameForAI(tool);
        this.validateDescriptionForHuman(tool);
        this.validateDescriptionForAI(tool);
        this.validateApiType(tool);
        this.validateApiUrl(tool);
        this.validateLogoUrl(tool);
        this.validateContactEmail(tool);
        this.validateLegalInfoUrl(tool);
    }

    static validateNameForHuman(tool: ToolType): void {
        // Add validation logic here
        if (!tool.name_for_human) {
            throw new Error('Name for human is required');
        }
    }

    static validateNameForAI(tool: ToolType): void {
        // Add validation logic here
        if (!tool.name_for_ai) {
            throw new Error('Name for AI is required');
        }
    }

    static validateDescriptionForHuman(tool: ToolType): void {
        // Add validation logic here
        if (!tool.description_for_human) {
            throw new Error('Description for human is required');
        }
    }

    static validateDescriptionForAI(tool: ToolType): void {
        // Add validation logic here
        if (!tool.description_for_ai) {
            throw new Error('Description for AI is required');
        }
    }

    static validateApiType(tool: ToolType): void {
        // Add validation logic here
        if (!tool.api_type) {
            throw new Error('API type is required');
        }
    }

    static validateApiUrl(tool: ToolType): void {
        // Add validation logic here
        if (!tool.api_url) {
            throw new Error('API URL is required');
        }
    }

    static validateLogoUrl(tool: ToolType): void {
        // Add validation logic here
        if (!tool.logo_url) {
            throw new Error('Logo URL is required');
        }
    }

    static validateContactEmail(tool: ToolType): void {
        // Add validation logic here
        if (!tool.contact_email) {
            throw new Error('Contact email is required');
        }
    }

    static validateLegalInfoUrl(tool: ToolType): void {
        // Add validation logic here
        if (!tool.legal_info_url) {
            throw new Error('Legal info URL is required');
        }
    }

    toJSON(): ToolType {
        return this.tool;
    }

    async createInDB(supabase: SupabaseClient): Promise<PostgrestError | ToolType> {
        const { data, error } = await supabase.from('tools').insert(this.tool).select();
        if (error) {
            console.error('Error creating tool', error);
            return error;
        }
        else {
            const tool = data[0];
            console.log('Created tool', tool);
            this.update(tool);
            return tool;
        }
    }

    async updateInDB(supabase: SupabaseClient): Promise<PostgrestError | ToolType> {
        const tool = this.toJSON();
        const { error } = await supabase.from('tools').update(tool).eq('id', tool.id);
        if (error) {
            console.error('Error updating tool', error);
            return error;
        }
        return tool;
    }

    static async deleteInDB(supabase: SupabaseClient, id: string): Promise<PostgrestError | boolean> {
        if (!id) {
            throw new Error('Tool ID is required but not set');
        }
        const { error } = await supabase.from('tools').delete().eq('id', id);
        if (error) {
            console.error('Error deleting tool', error);
            return error;
        }
        return true;
    }

    static async getInDB(supabase: SupabaseClient, id: string): Promise<PostgrestError | ToolType> {
        if (!id) {
            throw new Error('Tool ID is required but not set');
        }
        const { data, error } = await supabase.from('tools').select('*').eq('id', id).single();
        if (error) {
            console.error('Error fetching tool', error);
            return error;
        }
        else {
            const tool = data;
            console.log('Fetched tool', tool);
            return tool;
        }
    }
}