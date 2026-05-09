<script>
	import { docsData } from '$lib/docsData';
	import { page } from '$app/stores';

	let { children } = $props();

	const docKeys = Object.keys(docsData);
</script>

<div class="flex min-h-screen">
	<!-- Sidebar -->
	<aside class="w-64 bg-slate-50 border-r border-slate-200 sticky top-0 h-screen overflow-y-auto">
		<div class="p-6">
			<h2 class="text-xs font-semibold text-slate-500 uppercase tracking-wider">
				Documentation
			</h2>
			<nav class="mt-4 space-y-4">
				{#each Object.entries(docsData) as [key, category]}
					<div>
						<a href="/docs/{key}" class="font-bold text-slate-900 block mb-1">
							{category.title}
						</a>

						{#if category.items}
							<div class="ml-4 border-l border-slate-200 pl-4 space-y-1">
								{#each Object.keys(category.items) as itemKey}
									<a
										href="/docs/{key}/{itemKey}"
										class="block text-sm text-slate-600 hover:text-blue-600
										{$page.params.item === itemKey ? 'text-blue-600 font-medium' : ''}"
									>
										{itemKey}
									</a>
								{/each}
							</div>
						{/if}
					</div>
				{/each}
			</nav>
		</div>
	</aside>

	<!-- Main View -->
	<main class="flex-1 bg-white">
		<div class="max-w-4xl mx-auto px-8 py-12">
			{@render children()}
		</div>
	</main>
</div>