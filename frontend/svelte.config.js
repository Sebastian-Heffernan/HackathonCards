import adapter from '@sveltejs/adapter-node'; // Changed from vercel

    /** @type {import('@sveltejs/kit').Config} */
    const config = {
        compilerOptions: {
            runes: ({ filename }) => (filename.split(/[/\\]/).includes('node_modules') ? undefined : true)
        },
        kit: {
            // adapter-node will create a 'build' folder that runs anywhere Node is installed
            adapter: adapter({
                out: 'build' 
            })
        }
    };

    export default config;