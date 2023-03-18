import AssetViewer from '../../components/AssetVeiwer';
/**
 * Component for creating new asset.
 *
 * @component
 * @example
  component 
  return(
	return <AssetViewer canEdit={true} isNew={true} />
  )
 
 */
 
const CreateAsset = () => {
	return <AssetViewer canEdit={true} isNew={true} />;
};

export default CreateAsset;
