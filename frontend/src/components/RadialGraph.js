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
					</h1 >
				);
			})}
		</div>
	);
};

export default RadialGraph;