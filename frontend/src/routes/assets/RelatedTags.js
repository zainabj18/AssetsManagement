import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {fetchRelatedTags } from '../../api';

import AssetTable from '../../components/assets/AssetTable';
const RelatedTags = () => {
	const { id } = useParams();
	const [assetsin, setAssets] = useState([]);
	const link_col={'count':{
		header: 'Tags in Common',
		canFilter:true,
	}};

	useEffect(() => {
		fetchRelatedTags(id).then((data)=>{ console.log(data.data);
			setAssets(data.data);});
	}, [])
	;
	return (<AssetTable assets={assetsin} setSelectedAssets={()=>{}} preSelIDs={[]} cols={link_col}/>);
};
 
export default RelatedTags;