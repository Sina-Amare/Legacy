<script lang="ts">
	import type { PageData } from './$types';
	import { writable } from 'svelte/store';
    import type { Game } from '$lib/types';

	export let data: PageData;

	// Use Svelte stores for reactive updates to game state
	const gameState = writable(data.game);
	const decisionNodeState = writable(data.decisionNode);

	let isLoadingDecision = false;

	/**
	 * Handles the player's choice, sends it to the backend,
	 * and updates the local state with the new game data.
	 * @param optionId The ID of the chosen option.
	 */
	async function handleDecision(optionId: number) {
		isLoadingDecision = true;
		try {
			const response = await fetch(`http://localhost:8000/api/v1/games/${$gameState.id}/decide`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ option_id: optionId })
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.detail || 'Failed to process decision');
			}

			const updatedGame: Game = await response.json();
			
			// Update the game state store, which will reactively update the UI
			gameState.set(updatedGame);

			// Fetch the next decision node based on the updated game state
			if (updatedGame.current_decision_node_id) {
				const nextDecisionResponse = await fetch(`http://localhost:8000/api/v1/decisions/${updatedGame.current_decision_node_id}`);
				if (nextDecisionResponse.ok) {
					const nextNode = await nextDecisionResponse.json();
					decisionNodeState.set(nextNode);
				} else {
					// Handle case where there is no next decision (end of branch)
					decisionNodeState.set(null);
				}
			} else {
				// Handle case where game ends
				decisionNodeState.set(null);
			}

		} catch (error) {
			console.error('Error making decision:', error);
			if (error instanceof Error) {
				alert(`خطا: ${error.message}`);
			} else {
				alert('یک خطای ناشناخته رخ داد');
			}
		} finally {
			isLoadingDecision = false;
		}
	}

    function getStatusColor(value: number): string {
        if (value < 30) return 'bg-red-600';
        if (value < 70) return 'bg-yellow-500';
        return 'bg-green-500';
    }
</script>

<div class="min-h-screen p-4 sm:p-8 flex flex-col items-center font-serif">
	<!-- Header / Resource Bar -->
    {#if $gameState}
	<header class="w-full max-w-7xl mb-8">
		<div class="bg-white/5 p-6 rounded-xl shadow-lg backdrop-blur-lg">
			<div class="grid grid-cols-2 md:grid-cols-5 gap-x-6 gap-y-4 items-center">
				<!-- Year -->
				<div class="text-center md:col-span-1">
					<span class="text-lg text-primary/70">سال</span>
					<p class="text-3xl font-bold text-accent-hover mt-1">
						{$gameState.current_year > 0 ? $gameState.current_year : Math.abs($gameState.current_year) + ' ق.م'}
					</p>
				</div>
                <!-- Stability -->
                <div class="md:col-span-1">
                    <div class="flex justify-between items-end mb-1"><span class="text-lg text-primary/80">ثبات</span><span class="font-bold text-xl text-primary">{$gameState.stability}%</span></div>
                    <div class="w-full bg-black/30 rounded-full h-4 overflow-hidden border border-white/10"><div class="h-full rounded-full transition-all duration-500 {getStatusColor($gameState.stability)}" style="width: {$gameState.stability}%"></div></div>
                </div>
                <!-- Treasury -->
                <div class="md:col-span-1">
                    <div class="flex justify-between items-end mb-1"><span class="text-lg text-primary/80">خزانه</span><span class="font-bold text-xl text-primary">{$gameState.treasury}</span></div>
                    <div class="w-full bg-black/30 rounded-full h-4 overflow-hidden border border-white/10"><div class="h-full rounded-full bg-amber-400" style="width: {Math.min(100, $gameState.treasury / 20)}%"></div></div>
                </div>
                <!-- Military -->
                <div class="md:col-span-1">
                    <div class="flex justify-between items-end mb-1"><span class="text-lg text-primary/80">قدرت نظامی</span><span class="font-bold text-xl text-primary">{$gameState.military_strength}</span></div>
                    <div class="w-full bg-black/30 rounded-full h-4 overflow-hidden border border-white/10"><div class="h-full rounded-full bg-blue-500" style="width: {Math.min(100, $gameState.military_strength / 2)}%"></div></div>
                </div>
                <!-- Religion -->
                <div class="md:col-span-1">
                    <div class="flex justify-between items-end mb-1"><span class="text-lg text-primary/80">نفوذ مذهبی</span><span class="font-bold text-xl text-primary">{$gameState.religious_influence}</span></div>
                    <div class="w-full bg-black/30 rounded-full h-4 overflow-hidden border border-white/10"><div class="h-full rounded-full bg-purple-500" style="width: {$gameState.religious_influence}%"></div></div>
                </div>
			</div>
		</div>
	</header>
    {/if}

	<!-- Main Decision/Narrative Area -->
	<main class="w-full max-w-4xl">
        {#if $decisionNodeState}
		<div class="bg-black/20 p-8 rounded-2xl border border-primary/20">
			<p class="text-2xl leading-loose text-primary/90 mb-8 text-justify">
				{$decisionNodeState.node_text}
			</p>
			<div class="border-t border-accent/30 pt-6">
				<h3 class="text-xl text-accent mb-4 font-bold">گزینه‌های پیش رو:</h3>
				<div class="space-y-4">
					{#each $decisionNodeState.options as option}
						<button
                            on:click={() => handleDecision(option.id)}
                            disabled={isLoadingDecision}
							class="w-full text-right bg-white/5 hover:bg-white/10 p-4 rounded-lg
								   border border-primary/20 transition-colors duration-200
                                   disabled:opacity-50 disabled:cursor-wait"
						>
							<span class="text-lg text-primary">{option.option_text}</span>
						</button>
					{/each}
				</div>
			</div>
		</div>
        {:else}
        <div class="text-center p-8 bg-black/20 rounded-2xl">
            <h2 class="text-4xl text-accent-hover font-bold">پایان این شاخه از تاریخ</h2>
            <p class="mt-4 text-xl text-primary/80">شما به انتهای این مسیر داستانی رسیده‌اید. می‌توانید بازی را از ابتدا شروع کرده و انتخاب‌های دیگری را بیازمایید.</p>
        </div>
        {/if}
	</main>
</div>