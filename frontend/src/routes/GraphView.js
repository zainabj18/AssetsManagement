import RadialGraph from '../components/graph/RadialGraph';

const GraphView = () => {

	let test_data = {
		points: [
			{
				id: 1,
				name: 'a'
			},
			{
				id: 2,
				name: 'asset b'
			},
			{
				id: 3,
				name: 'long name asset c'
			},
			{
				id: 4,
				name: 'long name asset d'
			},
			{
				id: 5,
				name: 'long name asset e'
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
			},
			{
				from: 5,
				to: [1]
			}
		]
	};

	return (
		<RadialGraph data={test_data} />
	);
};

export default GraphView;