import { docsData } from '$lib/docsData.ts';
import { error } from '@sveltejs/kit';

export function load({ params }) {
    const entry = docsData[params.category];

    if (!entry) {
        throw error(404, 'Documentation page not found');
    }

    let category = params.category;

    return {
        entry,
        category
    };
}
