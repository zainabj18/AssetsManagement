import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getRelatedAssetsGraphData } from '../../api';
import RadialGraph from '../../components/Graph/RadialGraph';

const AssetRelationGraph = () => {

	const { id } = useParams();

	const [data, set_data] = useState({ points: [], joins: [] });

	useEffect(() => {
		getRelatedAssetsGraphData(id).then(data => {
			set_data(data.data);
		});
	}, []);

	return (
		<RadialGraph data={data} show2WayInKey={false}/>
	);
};

export default AssetRelationGraph;