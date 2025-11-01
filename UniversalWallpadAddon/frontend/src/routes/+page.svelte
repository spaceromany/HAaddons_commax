<script lang="ts">
  import type { Readable } from 'svelte/store';

  const greeting = $state('Hello World') as unknown as Readable<string>;
</script>

<main class="page">
  <h1>{$greeting}</h1>
</main>

<style>
  .page {
    display: grid;
    place-items: center;
    min-height: 100vh;
    font-family:
      system-ui,
      -apple-system,
      BlinkMacSystemFont,
      'Segoe UI',
      sans-serif;
    background: linear-gradient(135deg, #0f172a, #1d4ed8);
    color: white;
  }

  h1 {
    font-size: clamp(2.5rem, 8vw, 5rem);
    font-weight: 700;
    letter-spacing: 0.05em;
    text-shadow: 0 0.5rem 2rem rgba(15, 23, 42, 0.5);
  }
</style>
