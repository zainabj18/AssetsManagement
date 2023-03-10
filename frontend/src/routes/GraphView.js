import RadialGraph from '../components/Graph/RadialGraph';

const GraphView = () => {

	let test_data = {
		points: [1, 2, 3, 4, 5],
		joins: [
			{
				from: 1,
				to: [2, 3, 4]
			},
			{
				from: 2,
				to: [1, 3, 4]
			},
			{
				from: 3,
				to: [1, 2]
			},
			{
				from: 4,
				to: [3]
			}
		]
	};

	return (
		<RadialGraph data={test_data} />
	);
};

export default GraphView;