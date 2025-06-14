<script lang="ts">
	import { onMount } from 'svelte';

	// A promise that will hold the result of our API call
	let dynastiesPromise: Promise<any[]>;

	onMount(() => {
		// This function runs once when the component is first mounted to the page.
		// It's the perfect place to fetch initial data.
		console.log('Fetching data from backend...');
		dynastiesPromise = fetch('http://localhost:8000/api/v1/dynasties').then((res) => {
			if (!res.ok) {
				throw new Error('Network response was not ok');
			}
			return res.json();
		});
	});
</script>

<main>
	<h1>Legacy: An Alternate History Simulator</h1>
	<h2>Available Dynasties</h2>

	{#await dynastiesPromise}
		<p>Loading historical data...</p>
	{:then dynasties}
		<ul>
			{#each dynasties as dynasty}
				<li>
					<strong>{dynasty.name}</strong> ({dynasty.start_year} to {dynasty.end_year})
					<p>{dynasty.description}</p>
				</li>
			{/each}
		</ul>
	{:catch error}
		<p style="color: red;">Error: {error.message}</p>
	{/await}
</main>

<style>
	main {
		font-family: sans-serif;
		max-width: 800px;
		margin: 2rem auto;
	}
	ul {
		list-style: none;
		padding: 0;
	}
	li {
		border: 1px solid #ccc;
		border-radius: 8px;
		padding: 1rem;
		margin-bottom: 1rem;
	}
</style>