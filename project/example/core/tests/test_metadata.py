import pytest


@pytest.mark.django_db(transaction=True)
def test_metadata(authenticated_api_client, image_file_geotiff):
    response = authenticated_api_client.get(
        f'/api/large-image/{image_file_geotiff.pk}/metadata?projection=EPSG:3857'
    )
    assert response.status_code == 200
    metadata = response.data
    assert metadata['levels'] == 9
    assert metadata['sizeX'] == metadata['sizeY']
    assert metadata['tileWidth'] == metadata['tileHeight']
    assert metadata['tileWidth'] == metadata['tileHeight']


@pytest.mark.django_db(transaction=True)
def test_metadata_s3(authenticated_api_client, s3_image_file_geotiff):
    response = authenticated_api_client.get(
        f'/api/large-image-s3/{s3_image_file_geotiff.pk}/metadata?projection=EPSG:3857'
    )
    assert response.status_code == 200
    metadata = response.data
    assert metadata['levels'] == 9
    assert metadata['sizeX'] == metadata['sizeY']
    assert metadata['tileWidth'] == metadata['tileHeight']
    assert metadata['tileWidth'] == metadata['tileHeight']


@pytest.mark.django_db(transaction=True)
def test_internal_metadata(authenticated_api_client, image_file_geotiff):
    response = authenticated_api_client.get(
        f'/api/large-image/{image_file_geotiff.pk}/internal_metadata'
    )
    assert response.status_code == 200
    metadata = response.data
    assert metadata['driverLongName']


@pytest.mark.django_db(transaction=True)
def test_bands(authenticated_api_client, image_file_geotiff):
    response = authenticated_api_client.get(f'/api/large-image/{image_file_geotiff.pk}/bands')
    assert response.status_code == 200
    bands = response.data
    assert isinstance(bands[1], dict)


@pytest.mark.django_db(transaction=True)
def test_band(authenticated_api_client, image_file_geotiff):
    response = authenticated_api_client.get(f'/api/large-image/{image_file_geotiff.pk}/band?band=1')
    assert response.status_code == 200
    band = response.data
    assert band['interpretation']