from gradio_client import Client

def generate_with_veo(prompt):
	client = Client("ginigen/VEO3-Free")
	result = client.predict(
			prompt=prompt,
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