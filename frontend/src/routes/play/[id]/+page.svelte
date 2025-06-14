<script lang="ts">
	import type { PageData } from './$types';
	import type { Game } from '$lib/types';
	import { goto } from '$app/navigation';

	export let data: PageData;
	const { dynasty } = data;
	let isLoading = false;

	/**
	 * Handles the click event for the "Start Adventure" button.
	 * It sends a POST request to the backend to create a new game session.
	 */
	async function handleStartGame() {
		isLoading = true;
		try {
			const response = await fetch('http://localhost:8000/api/v1/games/', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ dynasty_id: dynasty.id })
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.detail || 'Failed to create game session');
			}

			const newGame: Game = await response.json();
			console.log('New game created:', newGame);
			alert(`ماجراجویی جدید با شناسه ${newGame.id} برای شما آغاز شد!`);

			// In the future, we will navigate to the game dashboard:
			// await goto(`/dashboard/${newGame.id}`);
		} catch (error) {
			console.error('Error starting game:', error);
			if (error instanceof Error) {
				alert(`خطا در شروع بازی: ${error.message}`);
			} else {
				alert('خطا در شروع بازی: یک مشکل ناشناخته رخ داد');
			}
		} finally {
			isLoading = false;
		}
	}
</script>

<div class="min-h-screen p-4 sm:p-8 flex items-center justify-center">
	<div
		class="max-w-4xl w-full bg-white/5 rounded-2xl shadow-2xl backdrop-blur-lg overflow-hidden flex flex-col md:flex-row"
	>
		<img
			src={dynasty.image_url}
			alt={dynasty.name}
			class="w-full md:w-1/3 h-64 md:h-auto object-cover"
		/>

		<div class="p-8 flex flex-col justify-between text-center md:text-right w-full">
			<div>
				<h1 class="text-5xl font-bold text-accent-hover mb-4 font-serif">{dynasty.name}</h1>
				<p class="text-primary/90 text-xl leading-loose font-serif">
					{dynasty.opening_brief}
				</p>
			</div>

			<button
				on:click={handleStartGame}
				disabled={isLoading}
				class="mt-8 self-center w-full md:w-auto bg-accent text-background font-bold text-xl py-3 px-10 
                       rounded-lg hover:bg-accent-hover transform hover:scale-105 transition-all 
                       duration-200 disabled:bg-gray-600 disabled:cursor-not-allowed"
			>
				{#if isLoading}
					در حال آماده‌سازی...
				{:else}
					آغاز ماجراجویی
				{/if}
			</button>
		</div>
	</div>
</div>