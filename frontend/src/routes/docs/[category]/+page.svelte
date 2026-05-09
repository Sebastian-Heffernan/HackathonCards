<script>
	import DocViewer from '$lib/components/DocView.svelte';
  let { data } = $props();
</script>

<DocViewer data={data.entry} />
