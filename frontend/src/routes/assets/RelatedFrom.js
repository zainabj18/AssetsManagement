import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {fetchRelatedFrom} from '../../api';

import AssetTable from '../../components/assets/AssetTable';
const RelatedFrom = () => {
	const { id } = useParams();
	const [assetsin, setAssets] = useState([]);

	useEffect(() => {
		fetchRelatedFrom(id).then((data)=>{ console.log(data.data);
			setAssets(data.data);});
	}, [])
	;
	return (<AssetTable assets={assetsin} setSelectedAssets={()=>{}} preSelIDs={[]}/>);
};
 
export default RelatedFrom;