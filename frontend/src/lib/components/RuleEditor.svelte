<script lang="ts">
    import { onMount } from "svelte";
    import { EditorState } from "@codemirror/state";
    import { EditorView, basicSetup } from "codemirror";
    import { docsData } from "$lib/docsData";
    import { autocompletion, completeFromList } from "@codemirror/autocomplete";
    import { StreamLanguage } from "@codemirror/language";
    import { HighlightStyle, tags } from "@codemirror/highlight";
    import { syntaxHighlighting } from "@codemirror/language";

    export function focus() {
        view?.focus();
    }
    // Sets words from docsData as keywords to be autocompleted in the editor
    const keywords = Object.keys(docsData.instructions.items);
    const completions = keywords.map((k) => ({
        label: k,
        type: "keyword",
    }));
    let { value = $bindable("") } = $props();

    let container!: HTMLDivElement;
    let view: EditorView;

    const dslHighlight = StreamLanguage.define({
        token(stream) {
            if (stream.match(new RegExp(`\\b(${keywords.join("|")})\\b`))) {
                return "keyword";
            }

            stream.next();
            return null;
        },
    });
    // Initialize the CodeMirror editor when the component mounts
    onMount(() => {
        view = new EditorView({
            state: EditorState.create({
                doc: value,
                extensions: [
                    basicSetup,
                    dslHighlight,
                    EditorView.updateListener.of((v) => {
                        if (v.docChanged) {
                            value = v.state.doc.toString();
                        }
                    }),
                    autocompletion({
                        override: [completeFromList(completions)],
                    }),
                ],
            }),
            parent: container,
        });
        return () => {
            view.destroy();
        };
    });
</script>

<div bind:this={container} class="h-full w-full"></div>

<style>
    .cm-editor {
        height: 100%;
        font-size: 14px;
    }

    .cm-content {
        font-family: monospace;
        padding: 12px;
    }

    .cm-scroller {
        overflow: auto;
    }
</style>
