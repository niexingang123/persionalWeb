var dom = document.getElementById("earth");
		var myChart = echarts.init(dom);
		option = {
			  backgroundColor: "#000",
			  globe:{
			    baseTexture: "static/image/world.jpg",
			    heightTexture: "static/image/world.jpg",
			     displacementScale: 0.04,
			    environment: "static/image/starfield.jpg",
			    shading:"realistic",
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