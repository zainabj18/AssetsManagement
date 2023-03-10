import RadialGraph from '../components/RadialGraph';

const GraphView = () => {

	let test_data = [
		{
			from: 'a',
			to: 'b'
		},
		{
			from: 'b',
			to: 'a'
		},
		{
			from: 'a',
			to: 'c'
		},
		{
			from: 'c',
			to: 'a'
		},
		{
			from: 'b',
			to: 'c'
		},
		{
			from: 'a',
			to: 'd'
		},
		{
			from: 'b',
			to: 'd'
		},
		{
			from: 'd',
			to: 'c'
		}
	];

	return (
		<RadialGraph data={test_data} />
	);
};

export default GraphView;