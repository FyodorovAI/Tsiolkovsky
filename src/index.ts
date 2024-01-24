/**
 * @fileoverview This file contains the implementation of an Express API server with Swagger documentation.
 * @module index
 */

import { SupabaseClient, createClient, PostgrestError } from '@supabase/supabase-js';
import express, { Request, Response } from 'express';
import { Tool } from './models/tool';
import { HealthUpdate } from './models/health';
import dotenv from 'dotenv';

if (process.env['NODE_ENV'] !== 'production') { 
    const { error } = dotenv.config();
    if (error) {
        throw error
    }
}

// load environment variables from dotenv
if (!process || !process.env || !process.env.hasOwnProperty('SUPABASE_PROJECT_URL') || !process.env.hasOwnProperty('SUPABASE_API_KEY')) {
    throw new Error('Environment variables SUPABASE_PROJECT_URL and SUPABASE_API_KEY must be set');
}
const SUPABASE_PROJECT_URL: string = process.env['SUPABASE_PROJECT_URL'] || '';
const SUPABASE_API_KEY: string = process.env['SUPABASE_API_KEY'] || '';
const supabase: SupabaseClient = createClient(SUPABASE_PROJECT_URL, SUPABASE_API_KEY)

export const app = express();
const port = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

/**
 * Default route that returns a simple message.
 */
app.get('/', (_req: Request, res: Response) => {
    res.status(200).send('Tsiolkovsky API');
});

/**
 * Route for adding a new tool.
 */
app.post('/tools', async (req: Request, res: Response) => {
    const tool = new Tool(req.body)
    await tool.createInDB(supabase)
    .then((tool) => {
        res.status(201).json({ tool });
    })
    .catch((error) => {
        console.error('Error adding tool', error);
        res.status(500).json({ error });
    })
});
 
/**
 * Route for fetching all tools.
 */
app.get('/tools', async (_req: Request, res: Response) => {
    const { data, error } = await supabase.from('tools').select('*');
    if (error) {
        console.error('Error fetching tools', error);
        res.status(500).json({ error: error.message });
    } else {
        console.log('Fetched tools', data);
        res.status(200).json(data);
    }
});

/**
 * Route for fetching a specific tool by ID.
 */
app.get('/tools/:id', async (req: Request, res: Response) => {
    const { id } = req.params;
    const { data, error } = await supabase.from('tools').select('*').eq('id', id);
    if (error) {
        console.error('Error fetching tool with id', id, error);
        res.status(500).json({ error });
    } else if (!data || data.length === 0) {
        console.error(`Tool with id ${id} not found`);
        res.status(404).json({ error: 'Tool not found' });
    }else {
        const tool = data[0];
        console.log('Fetched tool', tool);
        res.status(200).json(tool);
    }
});

/**
 * Route for updating a tool.
 * @param req - The request object
 * @param res - The response object
 * @returns The response object
 * @throws An error if the tool is not found
 * @throws An error if the update is invalid
 * @throws An error if the update fails
 */
app.put('/tools/:id', async (req: Request, res: Response) => {
    const { id } = req.params;
    const tool = new Tool({ id, ...req.body })
    await tool.updateInDB(supabase)
        .then((tool) => {
            res.status(200).json(tool);
        })
        .catch((error) => {
            console.error('Error updating tool', error);
            res.status(500).json({ error });
        });
})

/**
 * Route for deleting a tool.
 * @param req - The request object
 * @param res - The response object
 * @returns The response object
 * @throws An error if the tool is not found
 * @throws An error if the deletion fails
 */
app.delete('/tools/:id', async (req: Request, res: Response) => {
    const { id } = req.params;
    if (!id) {
        throw new Error('Tool ID is required but not set');
    }
    await Tool.deleteInDB(supabase, id)
        .then(() => {
            console.log('Deleted tool with id', id);
            res.status(204).send();
        })
        .catch((error: PostgrestError) => {
            console.error('Error deleting tool', error);
            res.status(500).json({ error: error.message });
        });
});

/**
 * Route for sending a health check.
 * @param req - The request object
 * @param res - The response object
 * @returns The response object
 * @throws An error if the health check fails
 */
app.post('/tools/:id/health', async (req: Request, res: Response) => {
    const { id } = req.params;
    const healthUpdate = new HealthUpdate({ ...req.body, tool_id: id });
    await healthUpdate.saveHealthCheck(supabase)
        .then((healthUpdate) => {
            res.status(201).json(healthUpdate);
        })
        .catch((error) => {
            console.error('Error sending health check', error);
            res.status(500).json({ error });
        });
});

/**
 * Route for getting a tool's health checks.
 * @param req - The request object
 * @param res - The response object
 * @returns The response object
 */
app.get('/tools/:id/health', async (req: Request, res: Response) => {
    const { id } = req.params;
    await Tool.getInDB(supabase, id as string)
        .catch((error) => {
            console.error('Tool with id', id, 'not found while fetching health checks', error);
            res.status(404).json({ error: error.message });
        });

    // Get health checks
    await HealthUpdate.getHealthChecks(supabase, id as string)
        .then((healthUpdates) => {
            console.log('Fetched health checks for tool', id, healthUpdates);
            res.status(200).json(healthUpdates);
        })
        .catch((error) => {
            console.error('Error fetching health checks for tool', id, error);
            res.status(500).json({ error: error.message });
        });
})

// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});