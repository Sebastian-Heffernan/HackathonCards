<script>
    import InstructionViewer from '$lib/components/InstructionView.svelte';
    let { data } = $props();
</script>

<!-- Pass the instruction data down -->
<InstructionViewer instruction={data.instruction} />
