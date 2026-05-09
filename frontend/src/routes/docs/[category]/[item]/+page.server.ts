import { error } from '@sveltejs/kit';
import { docsData } from '$lib/docsData.ts';

export function load({ params }) {
    const { category, item } = params;
    const categoryData = docsData[category];
    
    if (!categoryData || !categoryData.items[item]) {
        throw error(404, "Instruction not found");
    }

    return {
        instruction: categoryData.items[item]
    };
}
