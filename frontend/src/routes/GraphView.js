import RadialGraph from '../components/RadialGraph';

const GraphView = () => {

	let test_data = {
		ab: {
			from: 'a',
			to: 'b'
		},
		ba: {
			from: 'b',
			to: 'a'
		},
		ac: {
			from: 'a',
			to: 'c'
		},
		ca: {
			from: 'c',
			to: 'a'
		},
		bc: {
			from: 'b',
			to: 'c'
		},
		ad: {
			from: 'a',
			to: 'd'
		},
		bd: {
			from: 'b',
			to: 'd'
		},
		dc: {
			from: 'd',
			to: 'c'
		}
	};

	return (
		<RadialGraph data={test_data} />
	);
};

export default GraphView;