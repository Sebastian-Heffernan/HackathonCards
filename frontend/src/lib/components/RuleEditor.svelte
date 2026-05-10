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
    import { linter } from "@codemirror/lint";
    import type { Diagnostic } from "@codemirror/lint";
    let theme = $state<"light" | "dark">("dark");
    const themeCompartment = new Compartment();
    const highLightCompartment = new Compartment();
    const editableCompartment = new Compartment();

    // Sets words from docsData as keywords to be autocompleted in the editor
    const keywords = Object.keys(docsData.instructions.items);
    const registries = [
        "$turnPlayer",
        "$selectedCardId",
        "$playerCount",
        "$turnCount",
        "$winner",
    ];
    const completions = [
        ...registries.map((r) => ({ label: r, type: "registry" })),
        ...keywords.map((k) => ({ label: k, type: "keyword" })),
    ];
    let { value = $bindable(""), editable = true } = $props();

    let container!: HTMLDivElement;
    let view: EditorView;

    const dslHighlight = StreamLanguage.define({
        token(stream) {
            if (stream.peek() === "#") {
                stream.skipToEnd();
                return "comment";
            }
            if (
                stream.match(
                    /\$(turnPlayer|selectedCardId|playerCount|turnCount|winner)\b/,
                )
            ) {
                return "variableName";
            }
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
        { tag: tags.comment, color: "#6b7280", fontStyle: "italic" },
        { tag: tags.variableName, color: "#16a34a", fontWeight: "bold" },
    ]);
    const darkHighlight = HighlightStyle.define([
        { tag: tags.keyword, color: "#ff8800" },
        { tag: tags.atom, color: "#6699ff" },
        { tag: tags.comment, color: "#64784b", fontStyle: "italic" },
        { tag: tags.variableName, color: "#22c55e", fontWeight: "bold" },
    ]);
    const lightTheme = EditorView.theme({
        "&": {
            backgroundColor: "#ffffff",
            color: "#111827",
        },
        ".cm-cursor": {
            borderLeftColor: "#111827",
        },
        ".cm-tooltip": {
            backgroundColor: "#ffffff",
            color: "#111827",
            border: "1px solid #e5e7eb",
        },

        ".cm-tooltip-autocomplete": {
            backgroundColor: "#ffffff",
            color: "#111827",
        },

        ".cm-completionLabel": {
            color: "#111827",
        },

        ".cm-completionMatchedText": {
            color: "#2563eb",
            fontWeight: "bold",
        },  
        ".cm-tooltip-autocomplete > ul": {
                fontFamily: "monospace",
                margin: 0,
                padding: 0,
            },

            ".cm-tooltip-autocomplete > ul > li": {
                padding: "4px 8px",
            },

            ".cm-tooltip-autocomplete > ul > li[aria-selected]": {
                backgroundColor: "#2563eb",
                color: "#ffffff",
            },
        },
    );
    const darkTheme = EditorView.theme({
        "&": {
            backgroundColor: "#0f172a",
            color: "#e2e8f0",
        },
        ".cm-cursor": {
            borderLeftColor: "#e2e8f0",
        },
        ".cm-tooltip": {
            backgroundColor: "#0f172a",
            color: "#e2e8f0",
            border: "1px solid #334155",
        },

        ".cm-tooltip-autocomplete": {
            backgroundColor: "#0f172a",
            color: "#e2e8f0",
        },

        ".cm-completionLabel": {
            color: "#e2e8f0",
        },

        ".cm-completionMatchedText": {
            color: "#38bdf8",
            fontWeight: "bold",
        },
        ".cm-tooltip-autocomplete > ul": {
            fontFamily: "monospace",
            margin: 0,
            padding: 0,
            backgroundColor: "#0f172a",
        },

        ".cm-tooltip-autocomplete > ul > li": {
            padding: "4px 8px",
            backgroundColor: "#0f172a",
            color: "#e2e8f0",
        },

        ".cm-tooltip-autocomplete > ul > li[aria-selected]": {
            backgroundColor: "#1d4ed8",
            color: "#ffffff",
        },
    });
    const highLightStyle = $derived(
        theme === "dark" ? darkHighlight : lightHighlight,
    );

    const commentLinter = linter((view) => {
        const diagnostics: Diagnostic[] = [];
        const lines = view.state.doc.toString().split("\n");
        lines.forEach((line, i) => {
            const trimmed = line.trim();
            if (trimmed.startsWith("#")) return;
            const commentIndex = line.indexOf("#");
            if (commentIndex !== -1) {
                diagnostics.push({
                    from: view.state.doc.line(i + 1).from + commentIndex,
                    to: view.state.doc.line(i + 1).to,
                    severity: "warning",
                    message:
                        "Inline comments are not supported. Put comments on their own line.",
                });
            }
        });
        return diagnostics;
    });

    // Initialize the CodeMirror editor when the component mounts
    onMount(() => {
        view = new EditorView({
            state: EditorState.create({
                doc: value,
                extensions: [
                    basicSetup,
                    dslHighlight,
                    commentLinter,
                    editableCompartment.of(EditorView.editable.of(editable)),
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

    $effect(() => {
        if (!view) return;

        view.dispatch({
            effects: editableCompartment.reconfigure(
                EditorView.editable.of(editable),
            ),
        });
    });

    $effect(() => {
        if (!view) return;
        const current = view.state.doc.toString();
        if (current !== value) {
            view.dispatch({
                changes: { from: 0, to: current.length, insert: value },
            });
        }
    });

    export function focus() {
        view?.focus();
    }

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

<div class="relative flex flex-col h-full min-h-0" data-theme={theme}>
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
    <div class="flex-1 min-w-0 min-h-0 overflow-hidden">
        <div bind:this={container} class="h-full w-full"></div>
    </div>
</div>

<style>
    :global(.cm-editor) {
        height: 100%;
    }

    :global(.cm-scroller) {
        height: 100%;
        overflow-x: auto;
        overflow-y: auto;
    }

    :global(.cm-tooltip.cm-tooltip-lint) {
        font-family: monospace;
    }

    :global([data-theme="dark"] .cm-tooltip-lint) {
        font-family: monospace;
        background: #0f172a;
        color: #e2e8f0;
        border: 1px solid #334155;
    }

    :global([data-theme="light"] .cm-tooltip-lint) {
        font-family: monospace;
        background: #ffffff;
        color: #111827;
        border: 1px solid #e5e7eb;
    }
</style>
