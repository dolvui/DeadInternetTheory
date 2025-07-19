from gradio_client import Client

def generate_with_veo(prompt):
	client = Client("ginigen/VEO3-Free")
	result = client.predict(
			prompt="Inside a misty swamp at dawn, a humanoid alligator dressed in a pressed suit holds a vintage microphone with one scaly hand. Opposite him stands Lily, a startled frog wearing a straw hat and a raincoat. The alligator reporter clears his throat and asks, “Lily, can you lend me a lily pad?” Both freeze, then burst into croaky laughter, the frog clutching her belly, the alligator wiping tears of mirth. Sunbeams filter through Spanish moss, highlighting droplets on their suits.",
			nag_negative_prompt="Static, motionless, still, ugly, bad quality, worst quality, poorly drawn, low resolution, blurry, lack of details",
			nag_scale=11,
			height=480,
			width=832,
			duration_seconds=4,
			steps=4,
			seed=2025,
			randomize_seed=True,
			enable_audio=True,
			audio_negative_prompt="music",
			audio_steps=25,
			audio_cfg_strength=4.5,
			api_name="/generate_video_with_audio"
	)
	return prompt