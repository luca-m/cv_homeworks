%
% Tumor microscopy segmentation exercise
%
%	imapath='tumor_microscopy_c.tif'
% 
function ret=cellseg(impath)
	% Cell est.dimension. Should determine it using granulometry pre analysis
	CELL_ESTIMATED_DIM=25; 
	TOP_ENANCHMENT=1;
	BOTTOM_ENANCHMENT=1;
	se1=strel('disk',CELL_ESTIMATED_DIM);
 
	cells=imread(impath);
	cells_original=cells;
 
 	% Enhanche local contrast for fg/bg distinction and
 	cells_enanch=en_local_constrast(cells,se1);
 	% A little constrast refinement
 	cells_enanch=en_local_constrast(cells_enanch,strel('square',3)); 
 	% Equalization
 	cells_enanch=imadjust(cells_enanch);
 	% Enhance local contrast around cells (fg/bg)
 	cells_reconstr=en_local_constrast(cells_enanch,se1);
 	% Enanche constrast through line neighborhood in order to maximize
 	% constrast between blobs separations (enhanche borders)
 	cells_reconstr=en_local_constrast(cells_reconstr,strel('line',0,CELL_ESTIMATED_DIM));
 	cells_reconstr=en_local_constrast(cells_reconstr,strel('line',90,CELL_ESTIMATED_DIM));
 	cells_reconstr=en_local_constrast(cells_reconstr,strel('line',120,CELL_ESTIMATED_DIM));
 	cells_reconstr=en_local_constrast(cells_reconstr,strel('line',60,CELL_ESTIMATED_DIM));
 	% A little constrast refinement
 	cells_reconstr=en_local_constrast(cells_reconstr,strel('square',3));
 	% Binarization using OTSU thresholding (FG/BG segmentation)
 	cells_morpho_r=im2bw(cells_reconstr,graythresh(cells_reconstr));
 	% Fill holes inside blobs
 	cells_morpho_r=imfill(cells_morpho_r,'holes');
 	% Remove small bridges
 	cells_morpho_r=imopen(cells_morpho_r,strel('square',5));
 	% extract perimeter
 	cells_morpho_perim=bwperim(cells_morpho_r,8);
 
 	figure
 	subplot(2,3,1),subimage(cells),title('original');
 	subplot(2,3,2),subimage(cells_enanch),title('local enanchment + equalization');
 	subplot(2,3,3),subimage(cells_reconstr),title('border enhanchment');
 	subplot(2,3,4),subimage(cells_morpho_r),title('thresholding and opening');
 	subplot(2,3,5),subimage(cells_morpho_perim),title('perimeter');
 	%subplot(2,3,6),subimage(cells_morpho_perim);

	ret.cells_adj=cells_enanch;
	ret.cells=cells_original;
	ret.reconstr=cells_reconstr;
	ret.enanch=cells_enanch;
end

function imen=en_local_constrast(imorig,se)
	top_r=imtophat(imorig,se);
	bot_r=imbothat(imorig,se);
	imen=imorig+top_r-bot_r;
end

function imres=smooth_image(imorig,se)
	tmp=imerode(imorig,se);
	imres=imreconstruct(tmp,imorig);
	tmp=imdilate(imres,se);
	imres=imreconstruct(tmp,imres);
end


