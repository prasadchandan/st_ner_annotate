<script lang="ts">
  import { Streamlit } from "./streamlit";
  import type { RenderData } from "./streamlit";
  import MarkedWord from "./components/MarkedWord.svelte";
  import { onMount, afterUpdate, onDestroy } from "svelte"

  let text: string = "";
  let ents: {
    start: number;
    end: number;
    label: string;
  }[] = [];
  export let label: string;
  export let disabled: boolean;
  let selectedText: Selection | null = null;
  let mounted = false;

  const onRender = (event: Event): void => {
    const data = (event as CustomEvent<RenderData>).detail;
    if (!mounted) {
      text = data.args["text"];
      ents = data.args["ents"];
      mounted = true;
    }
  };

  onMount(() => {
    Streamlit.setComponentReady();
    Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
    Streamlit.setFrameHeight();
  });

  afterUpdate(() => {
    Streamlit.setFrameHeight();
  });

  onDestroy(() => {
    Streamlit.events.removeEventListener(Streamlit.RENDER_EVENT, onRender);
  });

  const returnValuesToPython = (): void => {
    console.log(ents);
    Streamlit.setComponentValue(ents);
  }

  const addEntities = (text: string, words: string, label: string): void => {
    let regexp: RegExp = new RegExp(words, 'g');
    console.log(`Regex: ${regexp}`);
    let match;

    while ((match = regexp.exec(text)) != null) {
      ents.push({
        start: match.index,
        end: match.index + words.length,
        label: label
      });
    }

    ents.sort((l, r): number => {
      if (l.start < r.end) return -1;
      if (l.start > r.end) return 1;
      return 0;
    });

    ents = ents;
  }

  const handleMessage = (event): void => {
    ents.splice(event.detail.id, 1);
    ents = ents;
    returnValuesToPython();
  };

  function handleMouseup(event) {
    selectedText = window.getSelection();
    if (selectedText && selectedText.toString().length > 0) {
      console.log(`Selected text ${selectedText}`);
      addEntities(text, selectedText.toString(), label);
      returnValuesToPython();
    }
  }
</script>

<svelte:window on:mouseup={handleMouseup} />

<main {disabled}>
  {#each ents as { start, end, label }, i (start)}
    {#if i == 0}{text.substring(0, start)}{/if}
    <MarkedWord
      words={text.substring(start, end)}
      {label}
      id={i}
      on:message={handleMessage}
    />
    {#if i != ents.length - 1}
      {text.substring(end + 1, ents[i + 1]["start"] - 1)}
    {/if}
    {#if i == ents.length - 1}{text.substring(end)}{/if}
  {:else}
    <!-- this block renders when ents.length === 0 -->
    <p>loading...</p>
  {/each}
</main>

<style>
  main {
    padding: 1em;
    line-height: 2;
  }
</style>
