function delete_character(character_id)
{
	fetch('/delete-character', {
		method: 'POST',
		body: JSON.stringify({ character_id: character_id})
	})
	.then((_response) => {
		window.location.href = '/';
	});
}