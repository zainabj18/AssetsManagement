import { List,ListItem } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchAssetsinTag } from '../api';

const TagViewer = () => {
	const [assets, setAssets] = useState([]);
	const [type, setTag] = useState('');
	const { id } = useParams();

	useEffect(() => {
		fetchAssetsinTag(id).then((res)=>{setAssets(res.data.assets);
			setTag(res.data.tag);});
		console.log(assets);
	}, [id]);
    
	return ( <List bg='red'>
		{assets.map((val,index)=>(
			<ListItem key={index}>{val.name}</ListItem>
		))}
	</List> );
};
 
export default TagViewer;