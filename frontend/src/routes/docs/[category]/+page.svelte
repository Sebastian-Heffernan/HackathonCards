<script>
	import DocViewer from '$lib/components/DocView.svelte';
  let { data } = $props();
  console.log(data.category)
</script>

<DocViewer category={data.category} data={data.entry}  />
