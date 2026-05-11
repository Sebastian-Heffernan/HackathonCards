<script>
	import { docsData } from "$lib/docsData";
	import { page } from "$app/stores";

	let { children } = $props();

	const docKeys = Object.keys(docsData);

  let showSidebar = $state(true);
</script>

<div class="flex min-h-screen relative">
  <div class="w-12 h-full shrink-0 flex justify-center absolute top-2 {showSidebar ? "left-66" : "left-2"}">
    <button
      type="button"
      class="w-8 h-8 bg-gray-700 text-white rounded shadow flex items-center justify-center hover:bg-gray-600 font-bold z-100"
      onclick={() => (showSidebar = !showSidebar)}
      title={showSidebar ? "Hide vars" : "Show vars"}
    >
      {showSidebar ? "<" : ">"}
    </button>
  </div>
	<!-- Button -->
	<a
		href="/"
		class="absolute top-4 right-4 px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm font-semibold"
	>
		Home
	</a>
	<!-- Sidebar -->
	<aside
		class="min-w-64 max-w-64 bg-slate-50 border-r border-slate-200 top-0 h-screen overflow-y-auto {showSidebar ? "sticky" : "!hidden"}"
	>
		<div class="p-6">
			<h2
				class="text-xs font-semibold text-slate-500 uppercase tracking-wider"
			>
				Documentation
			</h2>
			<nav class="mt-4 space-y-4">
				{#each Object.entries(docsData) as [key, category]}
					<div>
						<a
							href="/docs/{key}"
							class="font-bold text-slate-900 block mb-1"
						>
							{category.title}
						</a>

						{#if category.items}
							<div
								class="ml-4 border-l border-slate-200 pl-4 space-y-1"
							>
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
