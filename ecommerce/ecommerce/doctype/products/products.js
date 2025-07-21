// Copyright (c) 2024, 3XG and contributors
// For license information, please see license.txt

frappe.ui.form.on('Products', {
	refresh: function(frm) {
		load_image_gallery(frm);
	}
});

function load_image_gallery(frm){
	const imageArray = JSON.parse(frm.doc.images);
	let galleryImages = ``; 
	// <p>No images</p>
	imageArray.forEach(row => {
		galleryImages += get_template(row);
	});
	galleryImages = (galleryImages=="")?"Not Found!": galleryImages;
	let gallery = `${get_stype()}<div class="image-gallery">${galleryImages}</div>`;
	frm.set_df_property("images_display", "options", gallery);
}
function get_stype(){
	return `
	<style>
		.image-gallery {
		display: flex;
		overflow-x: auto;
		padding: 10px;
		gap: 20px;
		border: 1px solid #ccc;
		}
		.image-card {
		min-width: 20px;
		text-align: center;
		font-family: Arial, sans-serif;
		}
		.image-card img {
		max-width: 50%;
		height: auto;
		border-radius: 8px;
		}
		.image-details {
		margin-top: 8px;
		font-size: 14px;
		color: #555;
		}
		.image-details strong {
		display: block;
		color: #333;
		}
	</style>`;
}
function get_template(row){ 
	return `
		<div class="image-card">
			<a href="${row.url}" target="_blank">
				<img alt="${row.type}" src="${row.url}">
			</a>
			<div class="image-details">
				<small>${row.alt}</small>
			</div>
		</div>
	`;
}