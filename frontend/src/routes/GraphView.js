import RadialGraph from '../components/Graph/RadialGraph';

const GraphView = () => {

	let test_data = {
		points: [
			{
				id: 1,
				name: 'a'
			},
			{
				id: 2,
				name: 'b'
			},
			{
				id: 3,
				name: 'c'
			},
			{
				id: 4,
				name: 'd'
			},
			{
				id: 5,
				name: 'e'
			}
		],
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