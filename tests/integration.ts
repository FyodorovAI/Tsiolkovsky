import request from 'supertest';
import { expect } from 'chai';
import { app } from './../src/index'
import { ToolType } from './../src/models/tool'; // import the ToolType type

describe('Test /tools endpoint', () => {
    it('should create a tool', async () => {
        const tool: ToolType = {
            name_for_human: 'Tool 1',
            name_for_ai: 'Tool 1',
            description_for_human: 'Description 1',
            description_for_ai: 'Description 1',
            api_type: 'apiType 1',
            api_url: 'apiUrl 1',
            logo_url: 'logoUrl 1',
            contact_email: 'contactEmail 1',
            legal_info_url: 'legalInfoUrl 1'
        };
        const res = await request(app)
            .post('/tools', tool);

        expect(res.statusCode).toEqual(200);
    });
        expect(res.body).toHaveProperty('message', 'Tool created');
    });
});