import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {fetchRelatedFrom, fetchRelatedTo} from '../../api';

import AssetTable from '../../components/assets/AssetTable';
const RelatedTo = () => {
	const { id } = useParams();
	const [assetsin, setAssets] = useState([]);

	useEffect(() => {
		fetchRelatedTo(id).then((data)=>{ console.log(data.data);
			setAssets(data.data);});
	}, [])
	;
	return (<AssetTable assets={assetsin} setSelectedAssets={()=>{}} preSelIDs={[]}/>);
};
 
export default RelatedTo;