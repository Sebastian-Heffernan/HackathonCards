<script lang="ts">
    import { onMount } from "svelte";
    import { EditorState } from "@codemirror/state";
    import { EditorView, basicSetup } from "codemirror";
    import { docsData } from "$lib/docsData";
    import { autocompletion, completeFromList } from "@codemirror/autocomplete";
    import { StreamLanguage } from "@codemirror/language";
    import { syntaxHighlighting, HighlightStyle } from "@codemirror/language";
    import { tags } from "@lezer/highlight";
    import { Compartment } from "@codemirror/state";
    let theme = $state<"light" | "dark">("dark");
    const themeCompartment = new Compartment();
    const highLightCompartment = new Compartment();

    export function focus() {
        view?.focus();
    }
    // Sets words from docsData as keywords to be autocompleted in the editor
    const keywords = Object.keys(docsData.instructions.items);
    const completions = keywords.map((k) => ({
        label: k,
        type: "keyword",
    }));
    let { value = $bindable(""), editable = true } = $props();

    let container!: HTMLDivElement;
    let view: EditorView;

    const dslHighlight = StreamLanguage.define({
        token(stream) {
            if (stream.match(/\bLABEL\b/)) {
                return "atom";
            }
            if (stream.match(new RegExp(`\\b(${keywords.join("|")})\\b`))) {
                return "keyword";
            }
            stream.next();
            return null;
        },
    });
    const lightHighlight = HighlightStyle.define([
        { tag: tags.keyword, color: "#2563eb", fontWeight: "bold" },
        { tag: tags.atom, color: "#f97316", fontWeight: "bold" },
    ]);
    const darkHighlight = HighlightStyle.define([
        { tag: tags.keyword, color: "#ff8800" },
        { tag: tags.atom, color: "#6699ff" },
    ]);
    const lightTheme = EditorView.theme({
        "&": {
            backgroundColor: "#ffffff",
            color: "#111827",
        },
        ".cm-cursor": {
            borderLeftColor: "#111827",
        },
    });
    const darkTheme = EditorView.theme({
        "&": {
            backgroundColor: "#0f172a",
            color: "#e2e8f0",
        },
        ".cm-cursor": {
            borderLeftColor: "#e2e8f0",
        },
    });
    const highLightStyle = $derived(
        theme === "dark" ? darkHighlight : lightHighlight,
    );

    // Initialize the CodeMirror editor when the component mounts
    onMount(() => {
        view = new EditorView({
            state: EditorState.create({
                doc: value,
                extensions: [
                    basicSetup,
                    dslHighlight,
                    themeCompartment.of(darkTheme),
                    highLightCompartment.of(syntaxHighlighting(darkHighlight)),
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

    function updateTheme() {
        if (!view) return;

        view.dispatch({
            effects: [
                themeCompartment.reconfigure(
                    theme === "dark" ? darkTheme : lightTheme,
                ),

                highLightCompartment.reconfigure(
                    syntaxHighlighting(
                        theme === "dark" ? darkHighlight : lightHighlight,
                    ),
                ),
            ],
        });
    }
    function toggleTheme() {
        theme = theme === "dark" ? "light" : "dark";
        updateTheme();
    }
</script>

<div class="relative flex flex-col h-full min-h-0">
    <!-- TOP RIGHT TOGGLE -->
    <div class="absolute right-6 top-2 z-10">
        <button
            onclick={() => toggleTheme()}
            class="px-2 py-1 rounded-full bg-gray-200 text-xs flex gap-2"
        >
            <span
                class={theme === "light"
                    ? "font-bold text-black"
                    : "text-gray-400"}
            >
                light
            </span>

            <span class="text-gray-400">|</span>

            <span
                class={theme === "dark"
                    ? "font-bold text-black"
                    : "text-gray-400"}
            >
                dark
            </span>
        </button>
    </div>

    <!-- EDITOR -->
    <div class="flex-1 min-h-0 overflow-hidden">
        <div bind:this={container} class="h-full w-full"></div>
    </div>
</div>

<style>
    :global(.cm-editor) {
        height: 100%;
    }

    :global(.cm-scroller) {
        height: 100%;
        overflow: auto;
    }

</style>
