import RadialGraph from '../components/RadialGraph';

const GraphView = () => {

	let test_data = [
		{
			from: 'a',
			to: ['b', 'c', 'd']
		},
		{
			from: 'b',
			to: ['a', 'c', 'd']
		},
		{
			from: 'c',
			to: ['a', 'b']
		},
		{
			from: 'd',
			to: ['c']
		},
		{
			from: 'e',
			to: []
		}
	];

	return (
		<RadialGraph data={test_data} />
	);
};

export default GraphView;