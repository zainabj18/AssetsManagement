const RadialGraph = ({ data }) => {

	const size = 400;
	const radius = size / 2;
	const center = radius;
	const textSize = 10;
	const angleSplit = Math.PI * 2 / data.length;

	const getY = (index) => {
		return -radius * Math.cos(index * angleSplit) + center;
	};

	const getX = (index) => {
		return radius * Math.sin(index * angleSplit) + center;
	};

	const getTransform = (index) => {
		let x = getX(index);
		let y = getY(index);
		return 'translate(' + x + 'px, ' + y + 'px)';
	};

	const setCurve = (line) => {
		let offset = 1;
		let offx = ((offset * center) + ((line.x2 + line.x1) * 0.5)) / (offset + 1);
		let offy = ((offset * center) + ((line.y2 + line.y1) * 0.5)) / (offset + 1);
		return 'M' + line.x1 + ' ' + line.y1 + ' Q ' + offx + ' ' + offy + ' ' + line.x2 + ' ' + line.y2;
	};

	const calcPoints = () => {
		let points = {};
		data.forEach((dataPoint, index) => {
			points[dataPoint.from] = index;
		});
		let coords = [];
		data.forEach((dataPoint, indexFrom) => {
			dataPoint.to.forEach((to) => {
				coords.push({ x1: getX(indexFrom), y1: getY(indexFrom), x2: getX(points[to]), y2: getY(points[to]) });
			});
		});
		return coords;
	};

	let lines = calcPoints();

	return (
		<div style={{ display: 'inline-block', height: size + 'px', width: size + 'px', backgroundColor: 'yellow' }}>
			{data.map((dataPoint, index) => {
				return (
					<h1
						key={index}
						style={{
							position: 'absolute',
							transform: getTransform(index)
						}}
					>
						{dataPoint.from + '->' + dataPoint.to}
					</h1>
				);
			})}
			<svg
				style={{
					position: 'absolute',
					height: size + 'px',
					width: size + 'px'
				}}
			>
				{lines.map((line, index) => {
					return (
						<path
							key={index}
							d={setCurve(line)}
							stroke='black'
							strokeWidth='1'
							strokeLinecap="round"
							fill="transparent">
						</path>
					);
				})}
			</svg>
		</div>
	);
};

export default RadialGraph;