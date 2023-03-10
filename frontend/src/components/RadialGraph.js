const RadialGraph = ({ data }) => {
	return (
		data.map((dataPoint, index) => {
			return (
				<h1 key={index}>{dataPoint.from + '->' + dataPoint.to}</h1>
			);
		})
	);
};

export default RadialGraph;