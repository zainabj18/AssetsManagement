import { useEffect, useState } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import {fetchRelatedProjects, fetchRelatedTags } from '../../api';

import AssetTable from '../../components/assets/AssetTable';
const RelatedProjects = () => {
	const location = useLocation();
	const { id } = useParams();
	const [assetsin, setAssets] = useState([]);
	const link_col={'count':{
		header: 'Projects in Common',
		canFilter:true,
	}};

	useEffect(() => {
		console.log(location);
		fetchRelatedProjects(id).then((data)=>{ console.log(data.data);
			setAssets(data.data);});
	}, [])
	;
	return (<AssetTable assets={assetsin} setSelectedAssets={()=>{}} preSelIDs={[]} cols={link_col}/>);
};
 
export default RelatedProjects;