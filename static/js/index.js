window.onload = function() {
	var broser_width = document.documentElement.clientWidth;
	var main = document.getElementById('main');
	main.style.cssText = 'width:' + broser_width + 'px;';
	var public_height = 'height:' + broser_width * 0.75 / 2 + 'px;';
	var image = document.getElementById('image');
	image.style.cssText = 'width:' + broser_width/2 + 'px;';
	image.style.cssText = 'height:' + broser_width * 0.75 / 2 + 'px;';
	var img = document.getElementById('img');
	img.style.cssText = 'width:' + broser_width/2 + 'px;';
	img.style.cssText = 'height:' + broser_width * 0.75 / 2 + 'px;';
	var box = document.getElementById('box');
	box.style.cssText = 'height:' + broser_width * 0.75 / 2 + 'px;';
	box.style.cssText = 'width:' + broser_width / 2 + 'px;';
	var earth = document.getElementById('earth');
	earth.style.cssText = 'height:' + broser_width * 0.75 * 0.68 / 2 + 'px;';
//画地球仪
	var dom = document.getElementById("earth");
	var myChart = echarts.init(dom);
	option = {
		backgroundColor: "#000",
		globe: {
			baseTexture: "static/image/world.jpg",
			heightTexture: "static/image/world.jpg",
			displacementScale: 0.04,
			environment: "static/image/starfield.jpg",
			shading: "realistic",
			realisticMaterial: {
				roughness: 0.9
			},
			postEffect: {
				enable: true
			},
			light: {
				main: {
					intensity: 5,
					shadow: true
				},
				ambientCubemap: {
					texture: "static/image/pisa.hdr",
					diffuseIntensity: 0.2
				}
			}
		}

	};
	if (option && typeof option === "object") {
		myChart.setOption(option, true);
	}
}