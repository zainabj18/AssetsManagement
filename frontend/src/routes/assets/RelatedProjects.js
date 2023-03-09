import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {fetchRelatedProjects, fetchRelatedTags } from '../../api';

import AssetTable from '../../components/AssetTable';
const RelatedProjects = () => {
	const { id } = useParams();
	const [assetsin, setAssets] = useState([]);
	const link_col={'count':{
		header: 'Projects in Common',
		canFilter:true,
	}};

	useEffect(() => {
		fetchRelatedProjects(id).then((data)=>{ console.log(data.data);
			setAssets(data.data);});
	}, [])
	;
	return (<AssetTable assets={assetsin} setSelectedAssets={()=>{}} preSelIDs={[]} cols={link_col}/>);
};
 
export default RelatedProjects;