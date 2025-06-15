<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type { PageData } from './$types';
	import { writable } from 'svelte/store';
	import type { Game } from '$lib/types';

	export let data: PageData;

	const gameState = writable<Game | null>(data.game);
	const isLoading = writable<boolean>(false);
	const viewMode = writable<'decision' | 'narrative'>(
		// If the game starts with a narrative, show it, otherwise show decision
		data.game?.last_narrative && !data.game?.current_story_text ? 'narrative' : 'decision'
	);

	let socket: WebSocket | null = null;

	onMount(() => {
		const gameId = $gameState?.id;
		if (!gameId) return;

		const wsUrl = `ws://localhost:8000/ws/${gameId}`;
		socket = new WebSocket(wsUrl);

		socket.onopen = () => console.log('WebSocket connection established.');
		socket.onmessage = (event) => {
			console.log('New game state received from server:', event.data);
			try {
				const updatedGame: Game = JSON.parse(event.data);
				gameState.set(updatedGame);
				viewMode.set('narrative');
				isLoading.set(false);
			} catch (e) {
				console.error("Failed to parse WebSocket message:", e);
				isLoading.set(false);
			}
		};
        
		return () => socket?.close();
	});

	async function handleDecision(optionKey: string) {
		isLoading.set(true);
		viewMode.set('narrative'); // Switch to narrative view immediately

		try {
			const currentGame = $gameState;
			if (!currentGame) return;

			const response = await fetch(`http://localhost:8000/api/v1/games/${currentGame.id}/decide`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ option_key: optionKey })
			});

			if (response.status !== 202) {
                // If the immediate response is not "Accepted", it's an error.
                const errorData = await response.json().catch(() => ({detail: "An unknown error occurred"}));
                throw new Error(errorData.detail);
            }
            // On success (202), we do nothing and wait for the WebSocket push.
		} catch (error) {
			if (error instanceof Error) {
				alert(`خطا: ${error.message}`);
			} else {
				alert('یک خطای ناشناخته رخ داد');
			}
			isLoading.set(false);
			viewMode.set('decision'); // Revert to decision view on error
		}
	}
    
    function proceedToNextTurn() {
        // Switch the view back to the decision card.
        // The new decision is already in our gameState.
        viewMode.set('decision');
    }

    function getStatusColor(value: number): string {
        if (value < 30) return 'bg-red-600/70';
        if (value < 70) return 'bg-yellow-500/70';
        return 'bg-green-500/70';
    }
</script>

<div class="min-h-screen p-4 sm:p-8 flex flex-col items-center font-serif">
	{#if $gameState}
        <header class="w-full max-w-7xl mb-8">
            <div class="bg-white/5 p-6 rounded-xl shadow-lg backdrop-blur-lg">
				<div class="grid grid-cols-2 md:grid-cols-5 gap-x-6 gap-y-4 items-center">
					<!-- Year -->
					<div class="text-center md:col-span-1">
						<span class="text-lg text-primary/70">سال</span>
						<p class="text-3xl font-bold text-accent-hover mt-1">
							{$gameState.current_year > 0
								? $gameState.current_year
								: Math.abs($gameState.current_year) + ' ق.م'}
						</p>
					</div>
					<!-- Stability -->
					<div class="md:col-span-1">
						<div class="flex justify-between items-end mb-1"><span class="text-lg text-primary/80">ثبات</span><span class="font-bold text-xl text-primary">{$gameState.stability}%</span></div>
						<div
							class="w-full bg-black/30 rounded-full h-4 overflow-hidden border border-white/10"
						>
							<div
								class="h-full rounded-full transition-all duration-500 {getStatusColor(
									$gameState.stability
								)}"
								style="width: {$gameState.stability}%"
							/>
						</div>
					</div>
					<!-- Treasury -->
					<div class="md:col-span-1">
						<div class="flex justify-between items-end mb-1">
							<span class="text-lg text-primary/80">خزانه</span><span class="font-bold text-xl text-primary">{$gameState.treasury}</span>
						</div>
						<div
							class="w-full bg-black/30 rounded-full h-4 overflow-hidden border border-white/10"
						>
							<div
								class="h-full rounded-full bg-amber-400"
								style="width: {Math.min(100, $gameState.treasury / 20)}%"
							/>
						</div>
					</div>
					<!-- Military -->
					<div class="md:col-span-1">
						<div class="flex justify-between items-end mb-1">
							<span class="text-lg text-primary/80">قدرت نظامی</span
							><span class="font-bold text-xl text-primary">{$gameState.military_strength}</span>
						</div>
						<div
							class="w-full bg-black/30 rounded-full h-4 overflow-hidden border border-white/10"
						>
							<div
								class="h-full rounded-full bg-blue-500"
								style="width: {Math.min(100, $gameState.military_strength / 2)}%"
							/>
						</div>
					</div>
					<!-- Religion -->
					<div class="md:col-span-1">
						<div class="flex justify-between items-end mb-1">
							<span class="text-lg text-primary/80">نفوذ مذهبی</span
							><span class="font-bold text-xl text-primary">{$gameState.religious_influence}</span>
						</div>
						<div
							class="w-full bg-black/30 rounded-full h-4 overflow-hidden border border-white/10"
						>
							<div
								class="h-full rounded-full bg-purple-500"
								style="width: {$gameState.religious_influence}%"
							/>
						</div>
					</div>
				</div>
			</div>
        </header>

        <main class="w-full max-w-4xl">
            {#if $viewMode === 'decision'}
                {#if $gameState.current_story_text && $gameState.current_options}
                    <!-- Decision Card -->
                    <div class="bg-black/20 p-8 rounded-2xl border border-primary/20">
                        <p class="text-2xl leading-loose text-primary/90 mb-8 text-justify">
                            {$gameState.current_story_text}
                        </p>
                        <div class="border-t border-accent/30 pt-6">
                            <div class="flex justify-between items-center mb-4">
								<h3 class="text-xl text-accent font-bold">گزینه‌های پیش رو:</h3>
								<button
									class="bg-white/10 text-primary/80 px-4 py-2 rounded-lg text-sm hover:bg-white/20 transition-colors cursor-not-allowed opacity-50"
									title="این قابلیت به زودی اضافه خواهد شد"
									disabled>مشورت با شورا</button
								>
							</div>
                            <div class="space-y-4">
                                {#each Object.entries($gameState.current_options) as [key, text]}
                                    <button on:click={() => handleDecision(key)} disabled={$isLoading} class="w-full text-right bg-white/5 hover:bg-white/10 p-4 rounded-lg border border-primary/20 transition-colors duration-200 disabled:opacity-50 disabled:cursor-wait">
                                        <span class="text-lg text-primary">{text}</span>
                                    </button>
                                {/each}
                            </div>
                        </div>
                    </div>
                {:else}
                    <!-- End of Branch Display -->
                    <div class="text-center p-8 bg-black/20 rounded-2xl">
                         <h2 class="text-4xl text-accent-hover font-bold">پایان این سرگذشت</h2>
                         <p class="mt-4 text-xl text-primary/80">
							شما به انتهای این مسیر داستانی رسیده‌اید. می‌توانید بازی را از ابتدا شروع کرده و
							انتخاب‌های دیگری را بیازمایید.
						</p>
                    </div>
                {/if}
            {:else}
                <!-- Narrative Display -->
                <div class="bg-primary/5 p-8 rounded-lg border-2 border-dashed border-accent/30 animate-fade-in">
                    <h3 class="text-xl text-accent mb-4 font-bold">روایت وقایع...</h3>
                    {#if $isLoading}
                        <div class="flex items-center space-x-3 space-x-reverse">
                            <div class="w-2 h-2 bg-accent rounded-full animate-pulse"></div>
                            <p class="text-2xl text-primary/80">وقایع‌نگار در حال ثبت تاریخ است...</p>
                        </div>
                    {:else}
                        <p class="text-2xl leading-loose text-primary text-justify">
                            {$gameState.last_narrative}
                        </p>
                        <div class="text-center mt-8">
                            <button on:click={proceedToNextTurn} class="bg-accent text-background font-bold text-lg py-2 px-8 rounded-lg hover:bg-accent-hover transform hover:scale-105 transition-all">
                                ادامه ماجراجویی
                            </button>
                        </div>
                    {/if}
                </div>
            {/if}
        </main>
    {/if}
</div>

<style>
	@keyframes fade-in {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
	.animate-fade-in {
		animation: fade-in 0.5s ease-out forwards;
	}
</style>
